#include "reservation_engine.h"
#include <vector>
#include <ctime>

// Dummy implementation: no access to DB from C++, simple rule: if start_ts % 2 == 0 -> conflict
extern "C" int check_conflict(int terrain_id, long start_ts, long end_ts) {
    (void)terrain_id; (void)end_ts;
    return (start_ts % 2 == 0) ? 1 : 0;
}
