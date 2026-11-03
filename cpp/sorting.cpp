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
#include "priority_queue.hpp"

namespace adm {
void quick_sort(Integers &values, std::size_t begin, std::size_t end) {
    // Three-way partition keeps duplicate-heavy inputs linear per level.
    while (end > begin + 1) {
        Integer pivot = values[begin + (end - begin) / 2];
        std::size_t less = begin, current = begin, greater = end;
        while (current < greater) {
            if (values[current] < pivot) {
                std::swap(values[less++], values[current++]);
            } else if (values[current] > pivot) {
                std::swap(values[current], values[--greater]);
            } else {
                ++current;
            }
        }
        // Recurse on the smaller partition, bounding stack usage by O(log n).
        if (less - begin < end - greater) {
            quick_sort(values, begin, less);
            begin = greater;
        } else {
            quick_sort(values, greater, end);
            end = less;
        }
    }
}

void merge_sort(Integers &values, Integers &buffer, std::size_t begin, std::size_t end) {
    if (end <= begin + 1) {
        return;
    }
    auto middle = begin + (end - begin) / 2;
    merge_sort(values, buffer, begin, middle);
    merge_sort(values, buffer, middle, end);
    std::size_t left = begin, right = middle;
    for (auto i = begin; i < end; ++i) {
        if (right == end || (left < middle && values[left] <= values[right])) {
            buffer[i] = values[left++];
        } else {
            buffer[i] = values[right++];
        }
    }
    std::copy(buffer.begin() + static_cast<std::ptrdiff_t>(begin),
              buffer.begin() + static_cast<std::ptrdiff_t>(end),
              values.begin() + static_cast<std::ptrdiff_t>(begin));
}

// namespace
Integers sort(const std::string &method, Integers values) {
    if (method == "insertion") {
        for (std::size_t i = 1; i < values.size(); ++i) {
            Integer item = values[i];
            std::size_t j = i;
            while (j > 0 && values[j - 1] > item) {
                values[j] = values[j - 1];
                --j;
            }
            values[j] = item;
        }
    } else if (method == "selection") {
        for (std::size_t i = 0; i < values.size(); ++i) {
            std::size_t smallest = i;
            for (std::size_t j = i + 1; j < values.size(); ++j) {
                if (values[j] < values[smallest]) {
                    smallest = j;
                }
            }
            std::swap(values[i], values[smallest]);
        }
    } else if (method == "quick") {
        quick_sort(values, 0, values.size());
    } else if (method == "heap") {
        MinHeap heap;
        for (Integer value : values) {
            heap.push(value);
        }
        for (auto &value : values) {
            value = heap.pop();
        }
    } else if (method == "merge") {
        Integers buffer(values.size());
        merge_sort(values, buffer, 0, values.size());
    } else {
        throw std::invalid_argument("unknown sorting method");
    }
    return values;
}

int binary_search(const Integers &values, Integer target) {
    require(std::is_sorted(values.begin(), values.end()), "binary search requires sorted input");
    std::size_t left = 0, right = values.size();
    while (left < right) {
        std::size_t middle = left + (right - left) / 2;
        if (values[middle] < target) {
            left = middle + 1;
        } else {
            right = middle;
        }
    }
    return left < values.size() && values[left] == target ? static_cast<int>(left) : -1;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        Integers values;
        Integer value;
        while (std::cin >> value) {
            values.push_back(value);
        }
        for (auto sorted : sort("merge", values)) {
            std::cout << sorted << " ";
        }
        std::cout << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
