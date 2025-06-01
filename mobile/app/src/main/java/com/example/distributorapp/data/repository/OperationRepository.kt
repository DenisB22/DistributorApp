package com.example.distributorapp.data.repository

import com.example.distributorapp.data.remote.OperationApi
import com.example.distributorapp.data.model.OperationsResponse
import retrofit2.Response

class OperationRepository(private val api: OperationApi) {
    suspend fun getOperations(
        token: String?,
        page: Int,
        limit: Int,
        partner_name: String?,
        good_name: String?,
        oper_name: String?,
        start_date: String?,
        end_date: String?
    ): Response<OperationsResponse> {
        return api.getOperations(
            "Bearer $token",
            page, limit,
            partner_name,
            good_name,
            oper_name,
            start_date,
            end_date
        )
    }
}