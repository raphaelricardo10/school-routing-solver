#include <iostream>
#include "routes.cpp"

void print_cromossome(int chromossome)
{
    std::cout << chromossome << ' ';
}

void print_individual(ga::Individual *individual)
{
    individual->chromossome.map(print_cromossome);
    std::cout << '\n';
}

int main()
{
    int popSize = 200;
    int qtyLocations = 15;
    int qtyRoutes = 3;
    int maxGenerations = 100;
    int selectionK = 3;
    float mutationRate = 0.65;

    ga::RoutingGA ga(maxGenerations, popSize, qtyLocations, qtyRoutes, selectionK, mutationRate);

    ga.run();

    return 0;
}