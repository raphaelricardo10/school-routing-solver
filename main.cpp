#include <iostream>
#include "genetic.cpp"

void print_cromossomes(int chromossome){
    std::cout << chromossome;
}

void print_individual(ga::Individual *individual){
    individual->genes.map(print_cromossomes);
    std::cout << '\n';
}

int main()
{
    int popSize = 5;
    int n = 100;

    ga::Population p(popSize, n);

    p.map(print_individual);

    return 0;
}