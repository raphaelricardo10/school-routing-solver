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
            randomizer.distribution = UniformIntDistribution(0, v.size() - 1);
            int index1 = randomizer.get_number();
            int index2 = randomizer.get_number();

            *this = Interval(v, index1, index2);
        }

        Interval(std::vector<int> &v, int bpIndex, RandomizerInt &randomizer)
        {
            std::vector<int> breakpoints;
            breakpoints.reserve(v.size() - bpIndex + 1);
            breakpoints.push_back(0);
            breakpoints.insert(breakpoints.begin() + 1, v.begin() + bpIndex, v.end());

            randomizer.distribution = UniformIntDistribution(0, breakpoints.size() - 1);
            
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
        int numberOfRoutes;
        int numberOfLocations;
        std::vector<std::vector<int>> distances;

        RoutingGA(int maxGenerations, int populationSize, int numLocations, int numRoutes, int selectionK, float mutationRate)
        {
            srand(time(0));
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
            for (int i = 0; i < individualSize; i++)
            {
                std::vector<int> v;
                for (int j = 0; j < i; j++)
                {
                    v.push_back(1 + (rand() % individualSize - 1));
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

            if (this->should_update_best(individual->fitness))
            {
                this->population.best = individual;
            }
        }

        void make_crossover(Individual *p1, Individual *p2)
        {
            Interval p1Interval(p1->chromossome.genes, this->numberOfLocations, this->randomizer);
            Interval p2Interval(p2->chromossome.genes, this->numberOfLocations, this->randomizer);

            std::vector<int> p1Part;
            Interval crossoverInterval(p1Interval, p1Part, this->randomizer);

            std::deque<int> p2Part(p2Interval.begin(), p2Interval.end());

            std::unordered_set<int> crossoverMap(crossoverInterval.begin(), crossoverInterval.end());

            int rotationOffset = p1Interval.size() / 2;
            rotate_deq(p2Part, rotationOffset);

            std::deque<int> offspring(p2->chromossome.genes.begin(), p2->chromossome.genes.begin() + this->numberOfLocations);

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
        }

        void run()
        {
            std::function<void(Individual *)> boundCallback = std::bind(&RoutingGA::calculate_fitness, this, std::placeholders::_1);
            this->population.map(boundCallback);

            Individual *p1, *p2;
            std::tie(p1, p2) = this->make_selection();

            this->make_crossover(p1, p2);
        }
    };
}
