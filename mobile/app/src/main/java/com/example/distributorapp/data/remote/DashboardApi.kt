package com.example.distributorapp.data.remote

import com.example.distributorapp.data.model.DashboardResponse
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Query

interface DashboardApi {

    @GET("microinvest/dashboard")
    suspend fun getDashboardData(
        @Query("period") period: String? = "7d", // Options: "7d", "3m", "1y", "custom"
        @Query("start_date") startDate: String? = null, // Required only for "custom" period
        @Query("end_date") endDate: String? = null      // Required only for "custom" period
    ): Response<DashboardResponse>
}