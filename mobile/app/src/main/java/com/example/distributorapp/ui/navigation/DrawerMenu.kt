package com.example.distributorapp.ui.navigation

import androidx.compose.material3.Divider
import androidx.compose.material3.ModalDrawerSheet
import androidx.compose.material3.NavigationDrawerItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun DrawerMenu(
    drawerItems: List<DrawerItem>,
    onDrawerItemClick: (DrawerItem) -> Unit,
    onLogout: () -> Unit
) {
    ModalDrawerSheet {
        drawerItems.forEach { item ->
            NavigationDrawerItem(
                label = { Text(item.title) },
                selected = false,
                onClick = { onDrawerItemClick(item) }
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