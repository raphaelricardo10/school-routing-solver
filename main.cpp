#include <iostream>
#include "routes.cpp"

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
    int maxGenerations = 100;

    ga::RoutingGA ga(maxGenerations, popSize, qtyLocations, qtyRoutes);

    ga.population.map(print_individual);

    for(int i=0; i<ga.distances.size(); i++){
        std::cout << "Line num: " << i << "\tdata: ";
        for(int j=0; j<ga.distances[i].size(); j++){
            std::cout << ga.distances[i][j] << " ";
        }
        std::cout << '\n';
    }

    ga.run();

    return 0;
}