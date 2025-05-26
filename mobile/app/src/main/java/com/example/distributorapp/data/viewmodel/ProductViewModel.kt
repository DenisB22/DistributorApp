package com.example.distributorapp.data.viewmodel
import android.util.Log
import com.example.distributorapp.data.repository.ProductRepository
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.distributorapp.data.UserPreferences
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import com.example.distributorapp.data.model.Product

class ProductViewModel(
    private val userPreferences: UserPreferences,
    private val repository: ProductRepository
) : ViewModel() {

    private val _products = MutableStateFlow<List<Product>>(emptyList())
    val products: StateFlow<List<Product>> = _products

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    fun searchProducts(name: String?, code: String?, bar_code: String?, page: Int = 1, page_size: Int = 20, field: String, query: String) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val token = userPreferences.getToken()
                token?.let {
                    val response = repository.getProducts(it, name, code, bar_code, page, page_size)
                    if (response.isSuccessful) {
                        _products.value = response.body()?.products ?: emptyList()
                    }
                } ?: run {
                    Log.e("ProductViewModel", "Token is null")
                    _products.value = emptyList()
                }
            } catch (e: Exception) {
                _products.value = emptyList()
            } finally {
                _isLoading.value = false
            }
        }
    }
}