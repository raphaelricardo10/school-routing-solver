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

    class Chromossome
    {
    public:
        std::vector<int> genes;

        void map(void (*func)(int))
        {
            for (auto i = this->genes.begin(); i != this->genes.end(); ++i)
            {
                func(*i);
            }
        }
    };

    class Individual
    {
    public:
        int fitness;
        Chromossome chromossome;

        Individual(std::vector<int> genes)
        {
            this->fitness = 0;
            this->chromossome.genes = genes;
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
            this->generate_individuals();
        }

        void map(void (*func)(Individual *))
        {
            for (auto i = this->individuals.begin(); i != this->individuals.end(); ++i)
            {
                func(&(*i));
            }
        }

        void generate_individuals()
        {
            this->permutator.shuffle();

            for (int i = 0; i < this->size; i++)
            {
                this->permutator.shuffle();
                Individual individual(this->permutator.vector);
                this->individuals.push_back(individual);
            }
        }

        void mutation();
        void crossover();
    };
}
