// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary and on error. Log error to console.
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // Convert only the letters in the word to lowercase.
        for (int i = 0; i < strlen(word); i++)
        {
            if ((word[i] >= 'a' && word[i] <= 'z') || (word[i] >= 'A' && word[i] <= 'Z'))
            {
                word[i] = tolower(word[i]);
            }
        }

        // Hash the word
        int p = hash(word);

        // Free up a location for the word node and get rid of garbage values.
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            // Return false if out of memory.
            return false;
        }

        // Set the word and next property
        strcpy(n->word, word);
        n->next = NULL;

        // Check if p-entry in hashtable already has a pointer to an item in the list.
        if (hashtable[p] == NULL)
        {
            // Point the hashtable to our new node
            hashtable[p] = n;
        }
        else
        {
            // Add n to the list
            node *tmp = hashtable[p];
            while (tmp->next != NULL)
            {
                tmp = tmp->next;
            }
            tmp->next = n;
        }
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    int count = 0;
    for (int i = 0; i < N; i++)
    {
        node *c = hashtable[i];
        while (c != NULL)
        {
            count++;
            c = c->next;
        }
    }
    return count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int i = hash(word);

    node *c = hashtable[i];
    while (c != NULL)
    {
        if (strcasecmp(c->word, word) == 0)
        {
            return true;
        }
        c = c->next;
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *c = hashtable[i];
        while (c != NULL)
        {
            node *tmp = c->next;
            free(c);
            c = tmp;
        }
    }
    return true;
}