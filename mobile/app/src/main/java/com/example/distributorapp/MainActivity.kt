package com.example.distributorapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.*
import androidx.lifecycle.lifecycleScope
import androidx.navigation.compose.rememberNavController
import com.example.distributorapp.data.UserPreferences
import com.example.distributorapp.ui.navigation.AppNavigation
import com.example.distributorapp.LoginScreen
import com.example.distributorapp.ui.theme.DistributorAppTheme
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val userPreferences = UserPreferences(this)

        setContent {
            var isLoggedIn by remember { mutableStateOf(false) }
            var token by remember { mutableStateOf<String?>(null) }

            LaunchedEffect(Unit) {
                // Collect from DataStore
                userPreferences.isLoggedIn.collect { loggedIn ->
                    isLoggedIn = loggedIn
                }
            }

            LaunchedEffect(Unit) {
                token = userPreferences.getToken()
            }

            val navController = rememberNavController()

            DistributorAppTheme {
                if (isLoggedIn && !token.isNullOrEmpty()) {
                    AppNavigation(
                        navController = navController,
                        isLoggedIn = true,
                        onLoginSuccess = {
                            lifecycleScope.launch {
                                userPreferences.setLoggedIn(true)
                                token = userPreferences.getToken()
                            }
                        },
                        onLogout = {
                            lifecycleScope.launch {
                                userPreferences.clearToken()
                                userPreferences.setLoggedIn(false)
                                userPreferences.saveToken("")
                                token = null
                            }
                        },
                        userPreferences = userPreferences
                    )
                } else {
                    LoginScreen(
                        onLoginSuccess = {
                            lifecycleScope.launch {
                                userPreferences.setLoggedIn(true)
                                token = userPreferences.getToken()
                            }
                        }
                    )
                }
            }
        }
    }
}
