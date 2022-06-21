#include <vector>
#include <bits/stdc++.h>
#include <algorithm>

namespace ga
{
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

    class Gene
    {
    public:
        std::vector<int> chromossomes;

        void map(void (*func)(int))
        {
            for (auto i = this->chromossomes.begin(); i != this->chromossomes.end(); ++i)
            {
                func(*i);
            }
        }
    };

    class Individual
    {
    public:
        int fitness;
        Gene genes;

        Individual(std::vector<int> genes)
        {
            this->fitness = 0;
            this->genes.chromossomes = genes;
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

        Population(int size, int n)
        {
            this->generation = 0;
            this->size = size;
            this->permutator = Permutator(n);
            this->generate_individuals(n);
        }

        void map(void (*func)(Individual *))
        {
            for (auto i = this->individuals.begin(); i != this->individuals.end(); ++i)
            {
                func(&(*i));
            }
        }

        void generate_individuals(int n)
        {
            this->permutator.shuffle();

            for (int i = 0; i < this->size; i++)
            {
                for (int j = 0; j < n; j++)
                {
                    this->permutator.shuffle();
                    Individual individual(this->permutator.vector);
                    this->individuals.push_back(individual);
                }
            }
        }

        void mutation();
        void crossover();
    };
}
