package com.example.distributorapp.data.remote

import com.example.distributorapp.data.model.OperationsResponse
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Query

interface OperationApi {
    @GET("microinvest/operations")
    suspend fun getOperations(
        @Header("Authorization") token: String,
        @Query("page") page: Int,
        @Query("limit") limit: Int = 20,
        @Query("partner_id") partner_id: Int?,
        @Query("good_id") good_id: Int?,
        @Query("oper_type") oper_type: Int?,
        @Query("start_date") start_date: String?,
        @Query("end_date") end_date: String?
    ): Response<OperationsResponse>
}