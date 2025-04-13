package com.example.distributorapp.data.repository

import com.example.distributorapp.data.remote.DashboardApi
import com.example.distributorapp.data.model.DashboardResponse
import retrofit2.Response

class DashboardRepository(private val api: DashboardApi) {

    /**
     * Fetches dashboard data based on either a predefined period
     * or a custom date range.
     *
     * @param period Predefined period ("week", "month", "year") — mutually exclusive with startDate & endDate
     * @param startDate Custom range start date (format: YYYY-MM-DD)
     * @param endDate Custom range end date (format: YYYY-MM-DD)
     * @return Dashboard response from API
     * @throws IllegalArgumentException if invalid parameter combination is passed
     */
    suspend fun getDashboardData(
        period: String? = "7d",
        startDate: String? = null,
        endDate: String? = null
    ): Response<DashboardResponse> {

        // Validate query params
        if (period.isNullOrBlank() && (startDate.isNullOrBlank() || endDate.isNullOrBlank())) {
            throw IllegalArgumentException("Either 'period' or both 'startDate' and 'endDate' must be provided.")
        }

        if (!period.isNullOrBlank() && (!startDate.isNullOrBlank() || !endDate.isNullOrBlank())) {
            throw IllegalArgumentException("'period' cannot be used together with 'startDate' or 'endDate'.")
        }

        // Make API call
        return api.getDashboardData(
            period = period,
            startDate = startDate,
            endDate = endDate
        )
    }
}
