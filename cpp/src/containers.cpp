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

#include <numeric>

namespace adm {
void MinHeap::push(Integer value) {
    values_.push_back(value);
    std::size_t child = values_.size() - 1;
    while (child > 0) {
        std::size_t parent = (child - 1) / 2;
        if (values_[parent] <= values_[child]) {
            break;
        }
        std::swap(values_[parent], values_[child]);
        child = parent;
    }
}
Integer MinHeap::pop() {
    require(!empty(), "empty heap");
    Integer result = values_.front();
    values_.front() = values_.back();
    values_.pop_back();
    std::size_t parent = 0;
    while (2 * parent + 1 < values_.size()) {
        std::size_t child = 2 * parent + 1;
        if (child + 1 < values_.size() && values_[child + 1] < values_[child]) {
            ++child;
        }
        if (values_[parent] <= values_[child]) {
            break;
        }
        std::swap(values_[parent], values_[child]);
        parent = child;
    }
    return result;
}
DisjointSet::DisjointSet(int n) {
    require(n >= 0, "negative set count");
    parent_.resize(n);
    size_.assign(n, 1);
    std::iota(parent_.begin(), parent_.end(), 0);
}
int DisjointSet::find(int vertex) {
    require(vertex >= 0 && static_cast<std::size_t>(vertex) < parent_.size(), "invalid set index");
    int root = vertex;
    while (parent_[root] != root) {
        root = parent_[root];
    }
    while (vertex != root) {
        int next = parent_[vertex];
        parent_[vertex] = root;
        vertex = next;
    }
    return root;
}
bool DisjointSet::unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b) {
        return false;
    }
    if (size_[a] < size_[b]) {
        std::swap(a, b);
    }
    parent_[b] = a;
    size_[a] += size_[b];
    return true;
}
void LinkedList::insert(Integer value) {
    auto node = std::make_unique<Node>(value);
    node->next = std::move(head_);
    head_ = std::move(node);
}
bool LinkedList::contains(Integer value) const {
    for (Node *node = head_.get(); node; node = node->next.get()) {
        if (node->value == value) {
            return true;
        }
    }
    return false;
}
bool LinkedList::erase(Integer value) {
    auto *link = &head_;
    while (*link && (*link)->value != value) {
        link = &(*link)->next;
    }
    if (!*link) {
        return false;
    }
    auto removed = std::move(*link);
    *link = std::move(removed->next);
    return true;
}
Integers LinkedList::values() const {
    Integers result;
    for (Node *node = head_.get(); node; node = node->next.get()) {
        result.push_back(node->value);
    }
    return result;
}
void BinarySearchTree::insert(Integer value) {
    auto *link = &root_;
    while (*link) {
        if ((*link)->value == value) {
            return;
        }
        link = value < (*link)->value ? &(*link)->left : &(*link)->right;
    }
    *link = std::make_unique<Node>(value);
}
bool BinarySearchTree::contains(Integer value) const {
    Node *node = root_.get();
    while (node) {
        if (node->value == value) {
            return true;
        }
        node = value < node->value ? node->left.get() : node->right.get();
    }
    return false;
}
bool BinarySearchTree::erase_node(std::unique_ptr<Node> &node, Integer value) {
    if (!node) {
        return false;
    }
    if (value < node->value) {
        return erase_node(node->left, value);
    }
    if (value > node->value) {
        return erase_node(node->right, value);
    }
    if (!node->left) {
        auto removed = std::move(node);
        node = std::move(removed->right);
    } else if (!node->right) {
        auto removed = std::move(node);
        node = std::move(removed->left);
    } else {
        Node *successor = node->right.get();
        while (successor->left) {
            successor = successor->left.get();
        }
        node->value = successor->value;
        erase_node(node->right, successor->value);
    }
    return true;
}
bool BinarySearchTree::erase(Integer value) {
    return erase_node(root_, value);
}
Integers BinarySearchTree::values() const {
    Integers result;
    std::function<void(const Node *)> visit = [&](const Node *node) {
        if (!node) {
            return;
        }
        visit(node->left.get());
        result.push_back(node->value);
        visit(node->right.get());
    };
    visit(root_.get());
    return result;
}
namespace {
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
} // namespace
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
Integers sentinel_insert(Integers sorted, Integer value) {
    require(std::is_sorted(sorted.begin(), sorted.end()), "insertion requires sorted input");
    // A boundary guard is safer than reserving a magic finite sentinel value.
    sorted.push_back(value);
    std::size_t position = sorted.size() - 1;
    while (position > 0 && sorted[position - 1] > value) {
        sorted[position] = sorted[position - 1];
        --position;
    }
    sorted[position] = value;
    return sorted;
}
} // namespace adm
