#include <functional>
#include <tuple>
#include "genetic.cpp"

namespace ga
{
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
        std::vector<std::vector<int>> distances;

        RoutingGA(int maxGenerations, int populationSize, int numLocations, int numRoutes, int selectionK, float mutationRate)
        {
            this->maxGenerations = maxGenerations;
            this->numberOfRoutes = numRoutes;
            this->selectionK = selectionK;
            this->mutationRate = mutationRate;
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

        void make_crossover(Individual *p1, Individual *p2){

        }

        void run()
        {
            std::function<void(Individual *)> boundCallback = std::bind(&RoutingGA::calculate_fitness, this, std::placeholders::_1);
            this->population.map(boundCallback);

            Individual *p1, *p2;
            std::tie(p1, p2) = this->make_selection();
        }
    };
}
