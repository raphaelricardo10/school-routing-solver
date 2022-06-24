#include <vector>
#include <bits/stdc++.h>
#include <algorithm>
#include <tuple>

namespace ga
{
    template <class T>
    int pick_random_element(T &v)
    {
        return rand() % (v.size() - 1);
    }

    class Breakpoint{
    private:
        bool is_zero(){
            return this->value == 0;
        }
    public:
        int value;

        Breakpoint(std::vector<int> &v, bool allowZero){
            this->value = pick_random_element<std::vector<int>>(v);;

            if(!allowZero){
                while(this->is_zero()){
                    this->value = pick_random_element<std::vector<int>>(v);
                }
            }
            else{
                this->value = pick_random_element<std::vector<int>>(v);
            }
        }
    };

    class BreakpointSet{
    private:
        std::unordered_map<int, int> map;

        bool is_repeated(Breakpoint &breakpoint){
            return this->map.count(breakpoint.value);
        }

    public:
        std::set<int> values;

        BreakpointSet(std::vector<int> &v, int qty){
            for (int i = 0; i < qty; i++)
            {
                Breakpoint bp = Breakpoint(v, false);
                while(this->is_repeated(bp)){
                    bp = Breakpoint(v, false);
                }

                this->map[bp.value] = bp.value;
                this->values.insert(bp.value);
            }
        }
    };

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
        void generate_breakpoints(int qty)
        {
            BreakpointSet breakpoints(this->chromossome.genes, qty);

            for (int breakpoint : breakpoints.values){
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
            this->generate_breakpoints(qtyBreaks);
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
    private:
        // Tournament selection
        int select_parent()
        {
            int winner = pick_random_element<std::vector<Individual>>(this->population.individuals);
            for (int i = 1; i < this->selectionK; i++)
            {
                int chosen = pick_random_element<std::vector<Individual>>(this->population.individuals);

                if (this->population.individuals[i].fitness < this->population.individuals[winner].fitness)
                {
                    winner = chosen;
                }
            }

            return winner;
        };

        void avoid_repeating_parents(int p1, int p2){
            while(p1 == p2){
                p2 = this->select_parent();
            }
        }

    public:
        int maxGenerations;
        int selectionK;
        float mutationRate;
        Population population;

        virtual void calculate_fitness(Individual *individual) = 0;
        virtual void make_crossover(Individual *p1, Individual *p2) = 0;

        auto make_selection()
        {
            int p1 = this->select_parent();
            int p2 = this->select_parent();

            avoid_repeating_parents(p1, p2);

            return std::make_tuple(&population.individuals[p1], &population.individuals[p2]);
        };
    };
}
