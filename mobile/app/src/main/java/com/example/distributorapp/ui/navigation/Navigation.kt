package com.example.distributorapp.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.example.distributorapp.data.UserPreferences
import com.example.distributorapp.ui.dashboard.DashboardScreen
import com.example.distributorapp.LoginScreen
import com.example.distributorapp.ui.partner.PartnerScreen
import com.example.distributorapp.ui.products.ProductScreen

sealed class Screen(val route: String) {
    object Login : Screen("login_screen")
    object Dashboard : Screen("dashboard_screen")
    object Partners : Screen("partner_screen")
    object Products: Screen("product_screen")
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
            DashboardScreen(
                userPreferences = userPreferences,
                onLogout = {
                    onLogout()
                    navController.navigate(Screen.Login.route) {
                        popUpTo(Screen.Dashboard.route) { inclusive = true }
                    }
                },
                navController = navController
            )
        }

        composable(route = Screen.Partners.route) {
            PartnerScreen(
                userPreferences = userPreferences,
                onLogout = {
                    onLogout()
                    navController.navigate(Screen.Login.route) {
                        popUpTo(Screen.Dashboard.route) { inclusive = true }
                    }
                },
                navController = navController
            )
        }

        composable(route = Screen.Products.route) {
            ProductScreen(
                userPreferences = userPreferences,
                onLogout = {
                    onLogout()
                    navController.navigate(Screen.Login.route) {
                        popUpTo(Screen.Dashboard.route) { inclusive = true }
                    }
                },
                navController = navController
            )
        }
    }
}