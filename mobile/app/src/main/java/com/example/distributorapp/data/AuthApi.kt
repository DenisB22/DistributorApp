package com.example.distributorapp.data

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface AuthApi {
    @POST("auth/login/json")
    fun login(@Body request: LoginRequest): Call<LoginResponse>
}
