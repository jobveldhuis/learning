#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

// Record preference if vote is valid
bool vote(int voter, int rank, string name)
{
    // Loop through all candidates and check for the name
    for (int c = 0; c < candidate_count; c++)
    {
        if (strcmp(name, candidates[c].name) == 0)
        {
            // Set preference to the number of candidate, not the name. This way we can use it later to talk to the candidate struct.
            preferences[voter][rank] = c;
            return true;
        }
    }
    // If name is not in the list, return false.
    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    // Loop through all voters
    for (int v = 0; v < voter_count; v++)
    {
        // Loop through the vote positions, until one has been found that has not been eliminated yet
        for (int c = 0; c < candidate_count; c++)
        {
            // Check if candidate is eliminated
            if (candidates[preferences[v][c]].eliminated == false)
            {
                candidates[preferences[v][c]].votes++;
                // Break the loop to avoid double votes
                break;
            }
        }
    }
    return;
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    // Check if the candidate has gotten more than 50% of the votes
    // Loop through candidates.
    for (int c = 0; c < candidate_count; c++)
    {
        // If the candidate has more than 50% of all votes, declare winner and return true.
        if (candidates[c].votes > (0.5 * voter_count))
        {
            printf("%s\n", candidates[c].name);
            return true;
        }
    }
    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    // Set the vote to the first candidate. This might not be best practice, but it works as long as there is at least one person in the election.
    int min = candidates[0].votes;
    // Loop through all the candidates
    for (int c = 1; c < candidate_count; c++)
    {
        // Check if the candidates votes are lower than the current minimum and if so, set the minimum to this new number.
        if (candidates[c].votes < min && candidates[c].eliminated == false)
        {
            min = candidates[c].votes;
        }
    }
    return min;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    // Loop through all the candidates still in the election
    for (int c = 0; c < candidate_count; c++)
    {
        if (candidates[c].eliminated == false && candidates[c].votes != min)
        {
            return false;
        }
    }
    return true;
}

// Eliminate the candidate (or candidiates) in last place
void eliminate(int min)
{
    for (int c = 0; c < candidate_count; c++)
    {
        if (candidates[c].votes == min && candidates[c].eliminated == false)
        {
            candidates[c].eliminated = true;
        }
    }

    return;
}
