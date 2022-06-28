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

        Interval(std::vector<int> &v)
        {
            int index1 = pick_random_element(v);
            int index2 = pick_random_element(v, index1);

            *this = Interval(&v, index1, index2);
        }

        Interval(std::vector<int> &v, std::vector<int> &breakpoints)
        {
            int start = pick_random_element<std::vector<int>>(breakpoints);
            int end = start < breakpoints.size() - 1 ? start + 1 : start - 1;

            *this = Interval(&v, breakpoints[start], breakpoints[end]);
        }

        auto begin(){
            return this->v->begin() + startIndex;
        }

        auto end(){
            return this->v->begin() + endIndex;
        }

        auto at(int pos){
            return this->v->begin() + startIndex + pos;
        }

        int size(){
            return this->endIndex - this->startIndex + 1;
        }

        void rotate_left(int n){
            for(int i = 0; i < n; i++){
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
            std::vector<int> p2Breaks = {0};
            for (int i = 0; i < this->numberOfRoutes; i++)
            {
                int breakIndex = this->numberOfLocations + i;
                p1Breaks.push_back(p1->chromossome.genes[breakIndex]);
                p2Breaks.push_back(p2->chromossome.genes[breakIndex]);
            }


            Interval p1Interval(p1->chromossome.genes, p1Breaks);
            Interval p2Interval(p2->chromossome.genes, p2Breaks);
            
            std::vector<int> p1Part(p1Interval.begin(), p1Interval.end() + 1);
            std::deque<int> p2Part(p2Interval.begin(), p2Interval.end() + 1);

            Interval crossoverInterval(p1Part);
            std::unordered_set<int> crossoverMap(crossoverInterval.begin(), crossoverInterval.end() + 1);

            int rotationOffset = p1Interval.size()/2;
            rotate_deq(p2Part, rotationOffset);

            std::deque<int> offspring(p2->chromossome.genes.begin(), p2->chromossome.genes.begin() + this->numberOfLocations);

            p2Part.insert(p2Part.begin() + crossoverInterval.startIndex, crossoverInterval.begin(), crossoverInterval.end() + 1);
            offspring.erase(offspring.begin() + p2Interval.startIndex , offspring.begin() + p2Interval.endIndex + 1);
            offspring.insert(offspring.begin() + p2Interval.startIndex, p2Part.begin(), p2Part.end());
            
            int i = -1;
            auto it = std::remove_if(offspring.begin(), offspring.end(), [crossoverMap, p2Interval, crossoverInterval, offspring, &i, &removed] (int elem) {
                i++;
                
                if(crossoverMap.find(elem) == crossoverMap.end()){
                    return false;
                }

                int intervalIndex = p2Interval.startIndex;
                if(i < intervalIndex + crossoverInterval.startIndex || i > intervalIndex + crossoverInterval.endIndex){
                    return true;
                }

                return false;
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
