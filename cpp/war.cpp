/* Copyright 2003-2020 by Steven S. Skiena; all rights reserved. 
Permission is granted for use in non-commerical applications
provided this copyright notice remains intact and unchanged.

These programs appear in my books:

"The Algorithm Design Manual" by Steven Skiena, second edition, Springer,
London 2008.  See out website www.algorist.com for additional information
or https://www.amazon.com/exec/obidos/ASIN/1848000693/thealgorith01-20

"Programming Challenges: The Programming Contest Training Manual"
by Steven Skiena and Miguel Revilla, Springer-Verlag, New York 2003.
See our website www.programming-challenges.com for additional information,
or https://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/
*/

#include "item.hpp"

namespace adm {
struct WarResult {
    std::string winner;
    int steps;
};

int encode_card(const std::string &card) {
    require(card.size() == 2, "card requires rank and suit");
    const std::string ranks = "23456789TJQKA", suits = "cdhs";
    auto rank = ranks.find(card[0]), suit = suits.find(card[1]);
    require(rank != std::string::npos && suit != std::string::npos, "unknown card");
    return static_cast<int>(rank * 4 + suit);
}

std::string decode_card(int card) {
    require(card >= 0 && card < 52, "card rank outside deck");
    const std::string ranks = "23456789TJQKA", suits = "cdhs";
    return std::string{ranks[card / 4], suits[card % 4]};
}

WarResult war(const std::vector<int> &first, const std::vector<int> &second, int limit) {
    require(limit >= 0, "negative War step limit");
    std::set<int> unique;
    for (const auto &deck : {first, second}) {
        for (int card : deck) {
            require(card >= 0 && card < 52 && unique.insert(card).second,
                    "invalid or duplicate card");
        }
    }
    std::deque<int> a(first.begin(), first.end()), b(second.begin(), second.end()), pot;
    bool facedown = false;
    int steps = 0;
    while (!a.empty() && !b.empty() && steps < limit) {
        ++steps;
        int x = a.front(), y = b.front();
        a.pop_front();
        b.pop_front();
        pot.push_back(x);
        pot.push_back(y);
        if (facedown) {
            facedown = false;
            continue;
        }
        if (x / 4 == y / 4) {
            facedown = true;
            continue;
        }
        auto &winner = x / 4 > y / 4 ? a : b;
        winner.insert(winner.end(), pot.begin(), pot.end());
        pot.clear();
    }
    if (!a.empty() && b.empty()) {
        return {"a", steps};
    }
    if (a.empty() && !b.empty()) {
        return {"b", steps};
    }
    return {"draw", steps};
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        std::cout << war({48}, {0}, 100).winner << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
