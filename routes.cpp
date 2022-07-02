#include <functional>
#include <tuple>
#include <deque>
#include <unordered_set>
#include "genetic.cpp"

namespace ga
{
    class Interval
    {
    public:
        int startIndex;
        int endIndex;
        std::vector<int> *v;

        Interval(std::vector<int> &v, int index1, int index2)
        {
            this->v = &v;
            this->startIndex = std::min(index1, index2);
            this->endIndex = std::max(index1, index2);
        }

        Interval(std::vector<int> &v, RandomizerInt &randomizer)
        {
            randomizer.set_range(v);
            int index1 = randomizer.get_number();
            int index2 = randomizer.get_number(index1);

            *this = Interval(v, index1, index2);
        }

        Interval(std::vector<int> &v, int bpIndex, RandomizerInt &randomizer)
        {
            std::vector<int> breakpoints;
            breakpoints.reserve(v.size() - bpIndex + 1);
            breakpoints.push_back(0);
            breakpoints.insert(breakpoints.begin() + 1, v.begin() + bpIndex, v.end());

            randomizer.set_range(breakpoints);

            int start = randomizer.get_number();
            int end = start < breakpoints.size() - 1 ? start + 1 : start - 1;

            *this = Interval(v, breakpoints[start], breakpoints[end]);
        }

        Interval(Interval &interval, std::vector<int> &v, RandomizerInt &randomizer)
        {
            v.insert(v.begin(), interval.begin(), interval.end());
            *this = Interval(v, randomizer);
        }

        std::vector<int>::iterator begin()
        {
            return this->v->begin() + startIndex;
        }

        std::vector<int>::iterator end()
        {
            return this->v->begin() + endIndex + 1;
        }

        std::vector<int>::iterator at(int pos)
        {
            return this->v->begin() + startIndex + pos;
        }

        int size()
        {
            return this->endIndex - this->startIndex + 1;
        }

        void rotate_left(int n)
        {
            for (int i = 0; i < n; i++)
            {
                this->v->insert(this->end() + 1, *this->begin());
                this->v->erase(this->begin());
            }
        }
    };

    class Crossover{
    private:
        bool initialized;
        int numberOfTrials;

        template <class _ContainerType, class _ElementType>
        bool isInContainer(_ContainerType container, _ElementType elem)
        {
            return container.find(elem) != container.end();
        }

        bool isInRange(int base, int start, int end, int value)
        {
            return value >= base + start && value <= base + end;
        }

    public:
        int maxOfTrials;
        Individual *parent1;
        Individual *parent2;
        Individual offspring;

        Crossover(){
            this->maxOfTrials = 0;
            this->parent1 = 0;
            this->parent2 = 0;
            this->numberOfTrials = 0;
            this->initialized = false;
        }

        Crossover(Individual &parent1, Individual &parent2, int maxOfTrials){
            this->parent1 = &parent1;
            this->parent2 = &parent2;
            this->maxOfTrials = maxOfTrials;
            this->initialized = true;
            this->numberOfTrials = 0;
        }

        bool is_acceptable(){
            if(!this->initialized){
                return false;
            }

            if(this->offspring.fitness == 0){
                return false;
            }

            if(this->numberOfTrials > this->maxOfTrials){
                return false;
            }

            if(this->offspring.fitness > this->parent1->fitness){
                return false;
            }

            if(this->offspring.fitness > this->parent2->fitness){
                return false;
            }

            return true;
        }

        void make_offspring(int bpIndex, RandomizerInt &randomizer){
            Interval p1Interval(this->parent1->chromossome.genes, bpIndex, randomizer);
            Interval p2Interval(this->parent2->chromossome.genes, bpIndex, randomizer);

            std::vector<int> p1Part;
            Interval crossoverInterval(p1Interval, p1Part, randomizer);

            std::deque<int> p2Part(p2Interval.begin(), p2Interval.end());

            std::unordered_set<int> crossoverMap(crossoverInterval.begin(), crossoverInterval.end());

            int rotationOffset = p1Interval.size() / 2;
            rotate_deq(p2Part, rotationOffset);

            std::deque<int> offspring(this->parent2->chromossome.genes.begin(), this->parent2->chromossome.genes.begin() + bpIndex);

            p2Part.insert(p2Part.begin() + crossoverInterval.startIndex, crossoverInterval.begin(), crossoverInterval.end());
            offspring.erase(offspring.begin() + p2Interval.startIndex, offspring.begin() + p2Interval.endIndex + 1);
            offspring.insert(offspring.begin() + p2Interval.startIndex, p2Part.begin(), p2Part.end());

            int i = -1;
            auto it = std::remove_if(offspring.begin(), offspring.end(), [&crossoverMap, &p2Interval, &crossoverInterval, &i, this](int elem)
                                     {
                i++;

                if(!this->isInContainer(crossoverMap, elem)){
                    return false;
                }

                if(!this->isInRange(p2Interval.startIndex, crossoverInterval.startIndex, crossoverInterval.endIndex, i)){
                    return true;
                }

                return false; });

            offspring.erase(it, offspring.end());
            offspring.insert(offspring.end(), this->parent2->chromossome.genes.begin() + bpIndex, this->parent2->chromossome.genes.end());

            if(offspring.size() != this->parent1->chromossome.genes.size()){
                int j = 0;
            }

            this->numberOfTrials++;
            this->offspring = Individual(std::vector<int>(offspring.begin(), offspring.end()));
        }
    };

    class RoutingGA : public GeneticBase
    {
    private:
        bool should_update_best(int fitness)
        {
            if (!this->population.best)
            {
                return true;
            }

            return fitness < this->population.best->fitness;
        }

    public:
        int numberOfRoutes;
        int numberOfLocations;
        std::vector<std::vector<int>> distances;

        RoutingGA(int maxGenerations, int populationSize, int numLocations, int numRoutes, int selectionK, float mutationRate)
        {
            this->maxGenerations = maxGenerations;
            this->numberOfRoutes = numRoutes;
            this->selectionK = selectionK;
            this->mutationRate = mutationRate;
            this->numberOfLocations = numLocations;
            this->population = Population(populationSize, numLocations, numRoutes);
            this->generate_distances(numLocations);
        }

        void generate_distances(int individualSize)
        {
            RandomizerInt randomizer(1, 100);
            for (int i = 0; i < individualSize; i++)
            {
                std::vector<int> v;
                for (int j = 0; j < i; j++)
                {
                    v.push_back(randomizer.get_number());
                }
                this->distances.push_back(v);
            }
        }

        void calculate_fitness(Individual *individual)
        {
            int totalDistance = 0;

            for (int i = 1; i < this->numberOfRoutes; i++)
            {
                int nextRoute = individual->chromossome.genes[i];
                int prevRoute = individual->chromossome.genes[i - 1];

                int x = std::max(nextRoute, prevRoute) - 1;
                int y = std::min(nextRoute, prevRoute) - 1;

                totalDistance += this->distances[x][y];
            }

            individual->fitness = totalDistance;
        }

        void run()
        {
            for(this->population.generation; this->population.generation < this->maxGenerations; this->population.generation++)
            {
                this->population.map([this] (Individual *individual){
                    this->calculate_fitness(individual);

                    if (this->should_update_best(individual->fitness))
                    {
                        this->population.best = individual;
                    }

                });

                int p1, p2;
                Crossover crossover1;
                Crossover crossover2;

                while(!crossover1.is_acceptable() && !crossover2.is_acceptable()){
                    std::tie(p1, p2) = this->make_selection();

                    crossover1 = Crossover(this->population.individuals[p1], this->population.individuals[p2], 5);
                    crossover2 = Crossover(this->population.individuals[p2], this->population.individuals[p1], 5);

                    for(int i = 0; i < 5; i++){
                        if(!crossover1.is_acceptable()){
                            crossover1.make_offspring(this->numberOfLocations, this->randomizer);
                            this->calculate_fitness(&crossover1.offspring);
                        }
                        if(!crossover2.is_acceptable()){
                            crossover2.make_offspring(this->numberOfLocations, this->randomizer);
                            this->calculate_fitness(&crossover2.offspring);
                        }
                    }
                }

                this->population.individuals[p1] = crossover1.offspring;
                this->population.individuals[p2] = crossover2.offspring;
            }
        }
    };
}
