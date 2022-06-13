#include <stdio.h>
int timer = 0;

// void resetTimer() {
//     timer = 0;
//     while(timer == 400){
//         timer = timer + 1;
// }}

// void main() {
//     int up, down = 1;
//     int prev_up, prev_down = 0;
//     int n = 0;
//     while(1){
//         scanf("%d", &n);
//         switch(n)
//         {
//             case 1: 
//             if (prev_down && up){
//                 prev_down = 0;
//                 void resetTimer();
//             }
//             prev_up = up;
//             break;
//             case 2:
//             if (prev_up && down){
//                 prev_up = 0;
//                 void resetTimer();
//             }
//             prev_down = down;
//             break;
//             case 3:
//             prev_down = 0;
//             prev_up = 0;
//             break;
//             default:
//             printf("Invalid");
//             break;
//         }
//     }
// }

// typedef enum{
//     START = 0,
//     MOVE_UP = 1,
//     MOVE_DOWN = 2,
//     STOP = 3,
// } state_t;

// typedef enum{
//     isPluggedIn = 0,
//     isPressedUp = 1,
//     isPressedDown = 2,
//     motoroff = 3,
// } event_t;

// typedef struct {
//     state_t source;
//     state_t destination;
//     event_t event;
// } stateTransition_t;

// const stateTransition_t transitionTable[] = {

//     {START, START, isPluggedIn },
//     {START, MOVE_UP, isPressedUp},
//     {START, MOVE_DOWN, isPressedDown},
//     {START, STOP, motoroff},

//     {MOVE_UP, START, isPluggedIn },
//     {MOVE_UP, MOVE_UP, isPressedUp},
//     {MOVE_UP, MOVE_DOWN, isPressedDown},
//     {MOVE_UP, STOP, motoroff},

//     {MOVE_DOWN, START, isPluggedIn },
//     {MOVE_DOWN, MOVE_UP, isPressedUp},
//     {MOVE_DOWN, MOVE_DOWN, isPressedDown},
//     {MOVE_DOWN, STOP, motoroff},

//     {STOP, START, isPluggedIn},
//     {STOP, STOP, isPressedUp},
//     {STOP, STOP, isPressedDown},
//     {STOP, STOP, motoroff},
// };

// int main() {
//     int i =0;
//     int next_state, current_state,current_event = 0;
//     for(i =0; i < 16; i++) {
//         if(transitionTable[i].source == current_state && transitionTable[i].source == current_event)
//         next_state = transitionTable[i].destination;
//         break;
//     }
//     return next_state;
// }

void start(void);
void stop(void);
void move_up(void);
void move_down(void);

void(*stateptr)() = start;

typedef enum{
    START = 0,
    MOVE_UP = 1,
    MOVE_DOWN = 2,
    STOP = 3,
} state_t;

typedef enum{
    isPluggedIn = 0,
    isPressedUp = 1,
    isPressedDown = 2,
    motoroff = 3,
} event_t;

typedef struct {
    state_t source;
    event_t event;
    void (*stateptr)(void);
} stateTransition_t;


void resetTimer() {
    timer = 0;
    while(timer == 400){
        timer = timer + 1;
    }
}

int isPressedUp() {
    return 1;
}

int isPressedDown() { 
    return 1;
}

void motorUp() {
    down = 0;
    up = 1;
}

void motorDown() {
    up = 0;
    dwon = 1;
}

void motorOff() {
    down = 0;
    up = 0;
}

void main() {
    int prev_up, prev_down = 0;
    int n = 0;
    while(1){
        scanf("%d", &n);
        switch(n)
        {
            case 1: 
            if (prev_down && up){
                prev_down = 0;
                void resetTimer();
            }
            prev_up = up;
            break;
            case 2:
            if (prev_up && down){
                prev_up = 0;
                void resetTimer();
            }
            prev_down = down;
            break;
            case 3:
            prev_down = 0;
            prev_up = 0;
            break;
            default:
            printf("Invalid");
            break;
        }
    }
}