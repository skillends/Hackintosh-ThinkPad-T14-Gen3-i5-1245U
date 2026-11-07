// Small, hardware-independent helpers for the optional T14 power experiment.
#pragma once
#include <stdint.h>

static inline bool xpPolicyHot(bool wasHot, int temperature, int trip = 85, int resume = 75) {
    if (temperature < 0 || temperature >= trip) return true;
    return wasHot && temperature > resume;
}

static inline uint32_t xpPolicyLimit(uint32_t current, uint32_t requested, bool hot) {
    // During the thermal pause, only reduce limits. Never undo a lower firmware limit.
    uint32_t effective = hot && (current & 0x8000U) && (current & 0x7FFFU) < requested ? current & 0x7FFFU : requested;
    return (current & ~0xFFFFU) | effective | 0x8000U;
}
