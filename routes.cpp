#include "genetic.cpp"

namespace ga
{
    class RoutingGA : public GeneticBase
    {
    public:
        std::vector<std::vector<int>> distances;
        
        RoutingGA(int maxGenerations, int populationSize, int numLocations, int numRoutes)
        {
            this->maxGenerations = maxGenerations;
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
    };
}
