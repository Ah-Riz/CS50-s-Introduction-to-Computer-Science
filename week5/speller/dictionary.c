// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
// const unsigned int N = 26;
#define N 26
unsigned int word_count = 0; // Global variable to keep track of the number of words loaded

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int index = hash(word);
    node *cursor = table[index];
    for (node *temp = cursor; temp != NULL; temp = temp->next)
    {
        // Compare the word in the node with the input word
        if (strcasecmp(temp->word, word) == 0)
        {
            return true; // Word found
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hashvalue = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        hashvalue += tolower(word[i]);
        hashvalue = (hashvalue * tolower(word[i])) % N;
    }
    return hashvalue;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }
    char word_buffer[LENGTH + 1];

    while (fscanf(source, "%s", word_buffer) != EOF)
    {
        // Create a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(source);
            return false;
        }

        strcpy(new_node->word, word_buffer);
        new_node->next = NULL;

        int index = hash(word_buffer);
        if (table[index] == NULL)
        {
            // If no node exists at this index, set the new node as the first node
            table[index] = new_node;
        }
        else
        {
            // If a node already exists, insert the new node at the beginning of the linked list
            new_node->next = table[index];
            table[index] = new_node;
        }
        word_count++;
    }
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp); // Free the memory allocated for the node
        }
        table[i] = NULL; // Set the pointer to NULL after freeing
    }
    return true;
}
