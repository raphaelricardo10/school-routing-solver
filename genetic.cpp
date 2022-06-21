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
    private:
        void generateBreakpoints(int qty)
        {
            int lowerLimit = 1;
            int upperLimit = this->chromossome.genes.size() - 1;

            for (int i = 0; i < qty; i++)
            {
                int breakpoint = lowerLimit + (rand() % upperLimit);
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
        std::vector<std::vector<int>> distances;
        int generation;
        int size;
        int mutation_rate;
        Individual *best;
        std::vector<Individual> individuals;

        Population(int size, int n, int qtyBreaks)
        {
            this->generation = 0;
            this->size = size;
            this->permutator = Permutator(n);
            this->generate_individuals(qtyBreaks);
            this->generate_distances(n);
        }

        void map(void (*func)(Individual *))
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

        void generate_distances(int individualSize){
            for(int i=0; i<individualSize; i++){
                std::vector<int> v;
                for(int j=0; j<i; j++){
                    v.push_back(1 + (rand() % individualSize - 1));
                }
                this->distances.push_back(v);
            }
        }
    };
}
