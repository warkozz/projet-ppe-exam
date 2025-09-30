cmake_minimum_required(VERSION 3.10)
project(reservation_engine)
add_library(reservation_engine SHARED reservation_engine.cpp)
set_target_properties(reservation_engine PROPERTIES OUTPUT_NAME "reservation_engine")
