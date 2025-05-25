package com.example.distributorapp.data

import com.example.distributorapp.data.remote.AuthApi
import com.example.distributorapp.data.remote.DashboardApi
import com.example.distributorapp.data.remote.AuthInterceptor
import com.example.distributorapp.data.remote.PartnerApi
import com.example.distributorapp.data.remote.ProductApi
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {
    // TODO: Should be updated with real URL
    private const val BASE_URL = "http://10.0.2.2:8000/"

    fun createAuthApi(): AuthApi {
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(AuthApi::class.java)
    }

    fun createDashboardApi(userPreferences: UserPreferences): DashboardApi {
        val client = OkHttpClient.Builder()
            .addInterceptor(AuthInterceptor(userPreferences))
            .build()

        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(DashboardApi::class.java)
    }

    fun createPartnerApi(userPreferences: UserPreferences): PartnerApi {
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(getOkHttpClient(userPreferences))
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(PartnerApi::class.java)
    }

    fun createProductApi(userPreferences: UserPreferences): ProductApi {
        val client = OkHttpClient.Builder()
            .addInterceptor(AuthInterceptor(userPreferences))
            .build()

        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ProductApi::class.java)
    }

    private fun getOkHttpClient(userPreferences: UserPreferences): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(AuthInterceptor(userPreferences))
            .build()
    }
}

