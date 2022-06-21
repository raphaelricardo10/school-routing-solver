#include <iostream>
#include "genetic.cpp"

void print_cromossome(int chromossome){
    std::cout << chromossome << ' ';
}

void print_individual(ga::Individual *individual){
    individual->chromossome.map(print_cromossome);
    std::cout << '\n';
}

int main()
{
    int popSize = 5;
    int qtyLocations = 10;
    int qtyRoutes = 3;

    ga::Population p(popSize, qtyLocations, qtyRoutes);

    p.map(print_individual);

    return 0;
}