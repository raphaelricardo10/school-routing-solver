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
        int start;
        int end;
        std::vector<int> *v;

        Interval(std::vector<int> *v, int index1, int index2)
        {
            this->v = v;
            this->start = std::min(index1, index2);
            this->end = std::max(index1, index2);
        }

        template <class T>
        T get_subvector()
        {
            T newV;

            for (int i = this->start; i <= this->end; i++)
            {
                newV.push_back(this->v->at(i));
            }

            return newV;
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
            std::vector<int> p2Breaks = {0};

            for (int i = 0; i < this->numberOfRoutes; i++)
            {
                int breakIndex = this->numberOfLocations + i;

                p1Breaks.push_back(p1->chromossome.genes[breakIndex]);
                p2Breaks.push_back(p2->chromossome.genes[breakIndex]);
            }

            Interval p1Interval = extract_random_part(p1->chromossome.genes, p1Breaks);
            Interval p2Interval = extract_random_part(p2->chromossome.genes, p2Breaks);

            std::vector<int> p1Part = p1Interval.get_subvector<std::vector<int>>();
            std::deque<int> p2Part = p2Interval.get_subvector<std::deque<int>>();

            Interval crossoverInterval = extract_random_part(p1Part);

            std::cout << crossoverInterval.v->at(0);

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
