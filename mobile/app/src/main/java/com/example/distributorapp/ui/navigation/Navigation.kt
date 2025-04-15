package com.example.distributorapp.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.example.distributorapp.LoginScreen
import com.example.distributorapp.data.UserPreferences
import com.example.distributorapp.ui.dashboard.DashboardScreen
import com.example.distributorapp.ui.layout.MainLayout

sealed class Screen(val route: String) {
    object Login : Screen("login_screen")
    object Dashboard : Screen("dashboard_screen")
}

@Composable
fun AppNavigation(
    navController: NavHostController,
    isLoggedIn: Boolean,
    onLoginSuccess: () -> Unit,
    onLogout: () -> Unit,
    userPreferences: UserPreferences
) {
    NavHost(
        navController = navController,
        startDestination = if (isLoggedIn) Screen.Dashboard.route else Screen.Login.route
    ) {
        composable(route = Screen.Login.route) {
            LoginScreen(
                onLoginSuccess = {
                    onLoginSuccess()
                    navController.navigate(Screen.Dashboard.route) {
                        popUpTo(Screen.Login.route) { inclusive = true }
                    }
                }
            )
        }

        composable(route = Screen.Dashboard.route) {
            MainLayout {
                DashboardScreen(
                    userPreferences = userPreferences,
                    onLogout = {
                        onLogout()
                        navController.navigate(Screen.Login.route) {
                            popUpTo(Screen.Dashboard.route) { inclusive = true }
                        }
                    }
                )
            }
        }
    }
}
