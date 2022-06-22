#include <vector>
#include <bits/stdc++.h>
#include <algorithm>

namespace ga
{
    int pick_random_element(std::vector<int> &v)
    {
        return 1 + rand() % (v.size() - 1);
    }

    class Permutator
    {
    private:
        std::vector<int> generate_vector(int n)
        {
            std::vector<int> v(n);

            for (int i = 0; i < n; i++)
                v[i] = i + 1;

            return v;
        }

    public:
        int n;
        std::vector<int> vector;

        Permutator() {}

        Permutator(int n)
        {
            this->vector = this->generate_vector(n);
        }

        void shuffle()
        {
            std::random_shuffle(this->vector.begin(), this->vector.end());
        }
    };

    class Chromossome
    {
    public:
        std::vector<int> genes;

        void map(std::function<void(int)> func)
        {
            for (auto i = this->genes.begin(); i != this->genes.end(); ++i)
            {
                func(*i);
            }
        }
    };

    class Individual
    {
    private:
        void generateBreakpoints(int qty)
        {
            for (int i = 0; i < qty; i++)
            {
                int breakpoint = pick_random_element(this->chromossome.genes);
                this->chromossome.genes.push_back(breakpoint);
            }
        }

    public:
        int fitness;
        Chromossome chromossome;

        Individual(std::vector<int> genes, int qtyBreaks)
        {
            this->fitness = 0;
            this->chromossome.genes = genes;
            this->generateBreakpoints(qtyBreaks);
        }
    };

    class Population
    {
    private:
        Permutator permutator;

    public:
        int generation;
        int size;
        Individual *best;
        std::vector<Individual> individuals;

        Population() {}

        Population(int size, int n, int qtyBreaks)
        {
            this->best = 0;
            this->generation = 0;
            this->size = size;
            this->permutator = Permutator(n);
            this->generate_individuals(qtyBreaks);
        }

        void map(std::function<void(Individual *)> func)
        {
            for (auto i = this->individuals.begin(); i != this->individuals.end(); ++i)
            {
                func(&(*i));
            }
        }

        void generate_individuals(int qtyBreaks)
        {
            this->permutator.shuffle();

            for (int i = 0; i < this->size; i++)
            {
                this->permutator.shuffle();
                Individual individual(this->permutator.vector, qtyBreaks);
                this->individuals.push_back(individual);
            }
        }
    };

    class GeneticBase
    {
    public:
        int maxGenerations;
        float mutationRate;
        Population population;
        
        virtual void calculate_fitness(Individual *individual) = 0;
    };
}
