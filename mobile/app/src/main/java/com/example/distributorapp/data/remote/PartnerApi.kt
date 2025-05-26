package com.example.distributorapp.data.remote

import com.example.distributorapp.data.model.PartnerResponse
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Query

interface PartnerApi {
    @GET("microinvest/partners")
        suspend fun getPartners(
            @Header("Authorization") token: String,
            @Query("page") page: Int,
            @Query("limit") limit: Int,
            @Query("company") company: String?,
            @Query("mol") mol: String?,
            @Query("phone") phone: String?,
            @Query("tax_no") tax_no: String?
        ): Response<PartnerResponse>
}