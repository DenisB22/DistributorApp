package com.example.distributorapp.data.repository

import com.example.distributorapp.data.remote.PartnerApi
import retrofit2.Response
import com.example.distributorapp.data.model.PartnerResponse

class PartnerRepository(private val api: PartnerApi) {
    suspend fun getPartners(
        token: String?,
        page: Int,
        limit: Int,
        company: String?,
        mol: String?,
        phone: String?,
        taxno: String?
    ): Response<PartnerResponse> {
        return api.getPartners(
            token = "Bearer $token",
            page = page,
            limit = limit,
            company = company,
            mol = mol,
            phone = phone,
            taxno = taxno
        )
    }
}