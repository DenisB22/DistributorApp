package com.example.distributorapp.data.remote

import com.example.distributorapp.data.model.ProductResponse
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Query

interface ProductApi {
    @GET("microinvest/products")
    suspend fun getProducts(
        @Header("Authorization") token: String,
        @Query("name") name: String? = null,
        @Query("code") code: String? = null,
        @Query("bar_code") bar_code: String? = null,
        @Query("offset") offset: Int = 0,
        @Query("limit") limit: Int = 20
    ): Response<ProductResponse>
}