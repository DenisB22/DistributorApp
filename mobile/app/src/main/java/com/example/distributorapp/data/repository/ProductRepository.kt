package com.example.distributorapp.data.repository

import com.example.distributorapp.data.model.ProductResponse
import com.example.distributorapp.data.remote.ProductApi
import retrofit2.Response

class ProductRepository(private val api: ProductApi) {
    suspend fun getProducts(
        token: String?,
        name: String?,
        code: String?,
        bar_code: String?,
        offset: Int,
        limit: Int
    ): Response<ProductResponse> {
        return api.getProducts("Bearer $token", name, code, bar_code, offset, limit)
    }
}
