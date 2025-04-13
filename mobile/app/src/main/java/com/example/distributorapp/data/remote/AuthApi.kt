package com.example.distributorapp.data.remote

import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

interface AuthApi {
    @POST("auth/login/json")
    suspend fun login(@Body request: LoginRequest): Response<LoginResponse>
}
