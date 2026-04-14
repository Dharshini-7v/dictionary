#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#define MAX_WORDS 10000
#define MAX_WORD_LEN 100
#define DICT_FILE "dictionary.txt"
int compare_strings(const void *a, const void *b) {
    return strcmp((char *)a, (char *)b);
}
int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Please enter a word to search.\n");
        return 1;
    }

    char target[MAX_WORD_LEN];
    strncpy(target, argv[1], MAX_WORD_LEN - 1);
    target[MAX_WORD_LEN - 1] = 0;
    for (int i = 0; target[i]; i++) target[i] = tolower(target[i]);

    FILE *fp = fopen(DICT_FILE, "r");
    if (!fp) {
        printf("Error: Dictionary file missing.\n");
        return 1;
    }

    char words[MAX_WORDS][MAX_WORD_LEN];
    int count = 0;
    char line[MAX_WORD_LEN];

    while (fgets(line, sizeof(line), fp) && count < MAX_WORDS) {
        line[strcspn(line, "\r\n")] = 0;
        if (strlen(line) > 0) {
            strncpy(words[count], line, MAX_WORD_LEN - 1);
            words[count][MAX_WORD_LEN - 1] = 0;
            for (int i = 0; words[count][i]; i++) words[count][i] = tolower(words[count][i]);
            count++;
        }
    }
    fclose(fp);

    // DAA: Sort before binary search
    qsort(words, count, MAX_WORD_LEN, compare_strings);

    // DAA: Binary Search Algorithm
    int left = 0, right = count - 1;
    while (left <= right) {
        int mid = (left + right) / 2;
        int cmp = strcmp(words[mid], target);
        if (cmp == 0) {
            printf("Word '%s' found at position %d in the dictionary (C Search).\n", target, mid);
            return 0;
        } else if (cmp < 0) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    printf("Word '%s' not found in the dictionary.\n", target);
    return 0;
}