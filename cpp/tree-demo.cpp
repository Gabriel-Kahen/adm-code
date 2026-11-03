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
#include "tree.hpp"

namespace adm {
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
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        BinarySearchTree tree;
        tree.insert(3);
        tree.insert(1);
        tree.insert(2);
        tree.erase(3);
        for (auto value : tree.values()) {
            std::cout << value << " ";
        }
        std::cout << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
