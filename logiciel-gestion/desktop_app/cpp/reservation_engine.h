#pragma once
#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif
extern "C" API int check_conflict(int terrain_id, long start_ts, long end_ts);
