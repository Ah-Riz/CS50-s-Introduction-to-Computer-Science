#include <stdio.h>
#include <cs50.h>
#include <ctype.h>

const int POINT_LIST[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
const int NUM_PLAYERS = 2;

string get_input();
string string2lower(string s);
int get_scores(string words);
string get_winner(int num_players, int scores[]);

int main(void){
    string words[NUM_PLAYERS];
    int scores[NUM_PLAYERS];
    for (int i = 0; i < NUM_PLAYERS; i++){
        words[i] = get_input(i);
        scores[i] = get_scores(words[i]);
        printf("Player %i: %i\n", i + 1, scores[i]);
    }
    get_winner(NUM_PLAYERS, scores);
}

string get_winner(int num_players, int scores[]){
    int winner[2] = {0, 0};
    for (int i = 0; i < num_players; i++){
        if (i == 0){
            winner[0] = i + 1;
            winner[1] = scores[i];
        }
        else if (scores[i] > winner[1]){
            winner[0] = i + 1;
            winner[1] = scores[i];
        }else if (scores[i] < winner[1]){
            continue;
        }
        else if (scores[i] == winner[1]){
            winner[0] = 0;
            winner[1] = 0;
        }
    }
    if (winner[0] == 0 && winner[1] == 0){
        printf("Tie!\n");
    }else{
        printf("Player %i wins!\n", winner[0]);
    }
}

int get_scores(string words){
    int score = 0;
    for (int i = 0; words[i] != '\0'; i++){
        if (words[i] >= 'a' && words[i] <= 'z'){
            score += POINT_LIST[words[i] - 'a'];
        }
    }
    return score;
}

string string2lower(string s){
    for (int i = 0; s[i] != '\0'; i++){
        s[i] = tolower(s[i]);
    }
    return s;
}

string get_input(int i){
    string word = string2lower(get_string("Player %i: ", (i + 1)));
    return word;
}