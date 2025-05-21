package com.example.distributorapp.ui.components

import androidx.compose.material3.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.runtime.*
import androidx.navigation.NavController
import com.example.distributorapp.ui.navigation.DrawerItem
import com.example.distributorapp.ui.navigation.DrawerMenu
import kotlinx.coroutines.launch
import androidx.compose.foundation.layout.PaddingValues

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScaffoldLayout(
    navController: NavController,
    drawerItems: List<DrawerItem>,
    onLogout: () -> Unit,
    screenTitle: String,
    content: @Composable (PaddingValues) -> Unit
) {
    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val scope = rememberCoroutineScope()

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            DrawerMenu(
                drawerItems = drawerItems,
                onDrawerItemClick = { item ->
                    scope.launch { drawerState.close() }
                    navController.navigate(item.route)
                },
                onLogout = {
                    onLogout()
                }
            )
        }
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("Distributor App") },
                    navigationIcon = {
                        IconButton(onClick = {
                            scope.launch { drawerState.open() }
                        }) {
                            Icon(Icons.Default.Menu, contentDescription = "Menu")
                        }
                    }
                )
            }
        ) { padding ->
            content(padding)
        }
    }
}