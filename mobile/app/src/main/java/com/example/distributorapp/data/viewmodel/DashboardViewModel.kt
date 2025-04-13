package com.example.distributorapp.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.distributorapp.data.RetrofitClient
import com.example.distributorapp.data.model.DashboardResponse
import com.example.distributorapp.data.repository.DashboardRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import android.util.Log
import com.example.distributorapp.data.UserPreferences


class DashboardViewModel(
    private val userPreferences: UserPreferences
) : ViewModel() {

    private val repository = DashboardRepository(
        RetrofitClient.createDashboardApi(userPreferences)
    )

    private val _dashboardData = MutableStateFlow<DashboardResponse?>(null)
    val dashboardData: StateFlow<DashboardResponse?> = _dashboardData

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    fun fetchDashboardData(
        // period: String? = "week",
        period: String? = "7d",
        startDate: String? = null,
        endDate: String? = null
    ) {
        viewModelScope.launch {
            try {
                _isLoading.value = true
                val response = repository.getDashboardData(period, startDate, endDate)
                if (response.isSuccessful) {
                    _dashboardData.value = response.body()
                } else {
                    // Handle API error if needed
                    val errorMsg = response.errorBody()?.string()
                    Log.e("DashboardVM", "API error: ${response.code()}: $errorMsg")
                    _dashboardData.value = null
                }
            } catch (e: Exception) {
                // Handle network error or exception
                _dashboardData.value = null
            } finally {
                _isLoading.value = false
            }
        }
    }
}
