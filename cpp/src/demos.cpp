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

#include "adm.hpp"

#include <set>

namespace adm {
std::vector<std::pair<int, int>> grid_order(const std::string &method, int rows, int columns) {
    require(rows >= 0 && columns >= 0, "negative grid dimension");
    std::vector<std::pair<int, int>> result;
    if (method == "row" || method == "snake") {
        for (int row = 0; row < rows; ++row) {
            for (int column = 0; column < columns; ++column) {
                result.emplace_back(row,
                                    method == "snake" && row % 2 ? columns - 1 - column : column);
            }
        }
    } else if (method == "column") {
        for (int column = 0; column < columns; ++column) {
            for (int row = 0; row < rows; ++row) {
                result.emplace_back(row, column);
            }
        }
    } else {
        require(method == "diagonal", "unknown grid order");
        for (Integer diagonal = 0; diagonal < static_cast<Integer>(rows) + columns - 1;
             ++diagonal) {
            for (Integer row = std::max<Integer>(0, diagonal - columns + 1);
                 row <= std::min<Integer>(rows - 1, diagonal); ++row) {
                result.emplace_back(static_cast<int>(row), static_cast<int>(diagonal - row));
            }
        }
    }
    return result;
}
int find_match(const std::string &pattern, const std::string &text) {
    if (pattern.size() > text.size()) {
        return -1;
    }
    for (std::size_t i = 0; i <= text.size() - pattern.size(); ++i) {
        std::size_t j = 0;
        while (j < pattern.size() && text[i + j] == pattern[j]) {
            ++j;
        }
        if (j == pattern.size()) {
            return static_cast<int>(i);
        }
    }
    return -1;
}
std::string replace_names(std::string text,
                          const std::vector<std::pair<std::string, std::string>> &rules) {
    for (const auto &[old_name, new_name] : rules) {
        require(!old_name.empty(), "replacement pattern must be nonempty");
        std::string changed;
        std::size_t cursor = 0;
        while (cursor < text.size()) {
            auto found = text.find(old_name, cursor);
            if (found == std::string::npos) {
                break;
            }
            changed += text.substr(cursor, found - cursor);
            changed += new_name;
            cursor = found + old_name.size();
        }
        changed += text.substr(cursor);
        text = std::move(changed);
    }
    return text;
}
std::vector<Suitor> rank_suitors(std::vector<Suitor> suitors) {
    auto key = [](const Suitor &suitor) {
        require(suitor.height >= 0 && suitor.weight >= 0, "negative suitor measurement");
        return std::make_tuple(std::abs(suitor.height - 180),
                               suitor.weight > 75 ? suitor.weight - 75 : -suitor.weight,
                               suitor.last, suitor.first);
    };
    for (const auto &suitor : suitors) {
        (void)key(suitor);
    }
    std::stable_sort(suitors.begin(), suitors.end(),
                     [&](const Suitor &a, const Suitor &b) { return key(a) < key(b); });
    return suitors;
}
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
