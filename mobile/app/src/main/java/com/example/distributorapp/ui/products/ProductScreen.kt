package com.example.distributorapp.ui.product

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.distributorapp.data.UserPreferences
import androidx.compose.ui.Alignment
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import com.example.distributorapp.ui.components.MainScaffoldLayout
import com.example.distributorapp.ui.navigation.DrawerItem
import androidx.navigation.NavController
import com.example.distributorapp.data.RetrofitClient
import com.example.distributorapp.data.repository.ProductRepository
import com.example.distributorapp.data.viewmodel.ProductViewModel
import com.example.distributorapp.data.viewmodel.ProductViewModelFactory


@Composable
fun ProductList(viewModel: ProductViewModel) {
    val products by viewModel.products.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    if (isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
    } else {
        if (products.isEmpty()) {
            Text(
                text = "Няма намерени продукти",
                modifier = Modifier.padding(16.dp)
            )
        } else {
            // SCROLLABLE COLUMN
            LazyColumn(
                verticalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp)
            ) {
                items(products) { product ->
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        elevation = CardDefaults.cardElevation(4.dp)
                    ) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Text("Име: ${product.name}")
                            Text("Код: ${product.code}")
                            Text("Баркод: ${product.barCode}")
                            Text("Цена: ${product.priceOut} лв")
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProductScreen(
    userPreferences: UserPreferences,
    onLogout: () -> Unit,
    navController: NavController
) {
    val api = RetrofitClient.createProductApi(userPreferences)
    val repository = ProductRepository(api)

    val viewModel: ProductViewModel = viewModel(
        factory = ProductViewModelFactory(repository, userPreferences)
    )

    LaunchedEffect(Unit) {
        viewModel.fetchProducts(
            offset=1,
            limit=20,
            name="",
            code="",
            bar_code=""
        )
    }

    val searchOptions = mapOf(
        "Име" to "name",
        "Код" to "code",
        "Баркод" to "bar_code",
    )

    var selectedOption by remember { mutableStateOf("Име") }
    var searchText by remember { mutableStateOf("") }

    val drawerItems = listOf(
        DrawerItem(title = "Dashboard", route = "dashboard_screen"),
        DrawerItem(title = "Partners", route = "partner_screen"),
        DrawerItem(title = "Products", route = "product_screen"),
        DrawerItem(title = "Operations", route = "operation_screen"),
        // We will add another screens here
    )

    MainScaffoldLayout(
        navController = navController,
        drawerItems = drawerItems,
        onLogout = onLogout,
        screenTitle = "Продукти"
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            var expanded by remember { mutableStateOf(false) }
            ExposedDropdownMenuBox(
                expanded = expanded,
                onExpandedChange = { expanded = !expanded }
            ) {
                TextField(
                    value = selectedOption,
                    onValueChange = {},
                    readOnly = true,
                    label = { Text("Търси по") },
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                    modifier = Modifier.menuAnchor()
                )

                ExposedDropdownMenu(
                    expanded = expanded,
                    onDismissRequest = { expanded = false }
                ) {
                    searchOptions.keys.forEach { option ->
                        DropdownMenuItem(
                            text = { Text(option) },
                            onClick = {
                                selectedOption = option
                                expanded = false
                            }
                        )
                    }
                }
            }

            TextField(
                value = searchText,
                onValueChange = { searchText = it },
                label = { Text("Стойност за търсене") },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Text),
                modifier = Modifier.fillMaxWidth()
            )

            Button(onClick = {
                val selectedField = searchOptions[selectedOption] ?: "name"
                val name = if (selectedField == "name") searchText else null
                val code = if (selectedField == "code") searchText else null
                val bar_code = if (selectedField == "bar_code") searchText else null

                viewModel.fetchProducts(
                    0,
                    20,
                    name,
                    code,
                    bar_code
                )
            }) {
                Text("Търси")
            }

            ProductList(viewModel)
        }
    }
}