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
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        std::cout << replace_names("old old", {{"old", "new"}}) << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
