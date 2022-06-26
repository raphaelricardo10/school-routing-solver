#include <functional>
#include <tuple>
#include <deque>
#include <ctime>
#include "genetic.cpp"

namespace ga
{
    class Interval
    {
    public:
        int startIndex;
        int endIndex;
        std::vector<int> *v;

        Interval(std::vector<int> *v, int index1, int index2)
        {
            this->v = v;
            this->startIndex = std::min(index1, index2);
            this->endIndex = std::max(index1, index2);
        }

        auto begin(){
            return this->v->begin() + startIndex;
        }

        auto end(){
            return this->v->begin() + endIndex;
        }

        int size(){
            return this->startIndex - this->endIndex + 1;
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

        Interval extract_random_part(std::vector<int> &v)
        {
            int index1 = pick_random_element(v);
            int index2 = pick_random_element(v);

            while(index1 == index2){
                index2 = pick_random_element(v);
            }

            Interval interval(&v, index1, index2);

            return interval;
        }

        Interval extract_random_part(std::vector<int> &v, std::vector<int> &breakpoints)
        {
            int start = pick_random_element<std::vector<int>>(breakpoints);
            int end = start < breakpoints.size() - 1 ? start + 1 : start - 1;

            Interval interval(&v, breakpoints[start], breakpoints[end]);

            return interval;
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
            std::vector<int> p1Breaks = {0};
            for (int i = 0; i < this->numberOfRoutes; i++)
            {
                int breakIndex = this->numberOfLocations + i;
                p1Breaks.push_back(p1->chromossome.genes[breakIndex]);
            }

            std::deque<int> offspring;
            std::unordered_map<int, int> offspring_map;
            for(int i = 0; i < this->numberOfLocations; i++){
                int gene = p2->chromossome.genes[i];
                offspring.push_back(gene);
                offspring_map[gene] = i;
            }

            Interval p1Interval = extract_random_part(p1->chromossome.genes, p1Breaks);

            int rotationOffset = p1Interval.size()/2;
            rotate_deq(offspring, rotationOffset);

            offspring.insert(offspring.begin() + p1Interval.startIndex, p1Interval.begin(), p1Interval.end());

            for(auto it = p1Interval.begin(); it != p1Interval.end(); ++it){
                int gene = *it;
                if(offspring_map.find(gene) != offspring_map.end()){
                    int index = offspring_map[gene] - rotationOffset;
                    if(index < 0){
                        index += offspring_map.size();
                    }

                    if(offspring_map[gene] >= p1Interval.startIndex){
                        index += p1Interval.startIndex - p1Interval.startIndex + 1;
                    }

                    offspring[index] = -1;
                }
            }

            auto it = std::remove_if(offspring.begin(), offspring.end(), [](int elem){
                return elem == -1;
            });
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
