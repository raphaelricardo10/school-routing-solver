#include <iostream>
#include "genetic.cpp"

int main()
{
    ga::Population p(10);

    for (int i = 0; i < p.individuals[0].genes.chromossomes.size(); i++)
    {
        std::cout << p.individuals[0].genes.chromossomes[i];
    }

    return 0;
}