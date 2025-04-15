package com.example.distributorapp.ui.navigation

import androidx.compose.material3.Divider
import androidx.compose.material3.ModalDrawerSheet
import androidx.compose.material3.NavigationDrawerItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.navigation.NavController

@Composable
fun DrawerMenu(
    navController: NavController,
    drawerItems: List<DrawerItem>,
    onLogout: () -> Unit
) {
    ModalDrawerSheet {
        drawerItems.forEach { item ->
            NavigationDrawerItem(
                label = { Text(item.title) },
                selected = false,
                onClick = {
                    navController.navigate(item.route) {
                        popUpTo(navController.graph.startDestinationId)
                        launchSingleTop = true
                    }
                }
            )
        }

        Divider()

        NavigationDrawerItem(
            label = { Text("Logout") },
            selected = false,
            onClick = { onLogout() }
        )
    }
}