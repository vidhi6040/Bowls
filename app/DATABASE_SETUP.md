## Database setup

## Setting up and using the database
USE bowls_db

## Establishing a collection (item_master) to store and manage menu item data
# Breakfast
db.item_master.insertMany([
    {
        item_code: "b1001",
        name: "Potato Finger",
        category: "breakfast",
        price: 3.5,
        image: "breakfast/b1001.png",
        available: true
    },
    {
        item_code: "b1002",
        name: "Steam Momo",
        category: "breakfast",
        price: 1.9,
        image: "breakfast/b1002.png",
        available: true
    },
    {
        item_code: "b1003",
        name: "Pig and Egg",
        category: "breakfast",
        price: 2.7,
        image: "breakfast/b1003.png",
        available: true
    },
    {
        item_code: "b1004",
        name: "Tomato Omlet",
        category: "breakfast",
        price: 2.4,
        image: "breakfast/b1004.png",
        available: true
    },
    {
        item_code: "b1005",
        name: "Fish JimJim",
        category: "breakfast",
        price: 3.0,
        image: "breakfast/b1005.png",
        available: true
    },
    {
        item_code: "b1006",
        name: "Yami Cheese",
        category: "breakfast",
        price: 1.8,
        image: "breakfast/b1006.png",
        available: true
    },
    {
        item_code: "b1007",
        name: "Finger Cheese",
        category: "breakfast",
        price: 1.9,
        image: "breakfast/b1007.png",
        available: true
    },
    {
        item_code: "b1008",
        name: "Fry Egg Spinach",
        category: "breakfast",
        price: 1.9,
        image: "breakfast/b1008.png",
        available: true
    },
    {
        item_code: "b1009",
        name: "Pasta",
        category: "breakfast",
        price: 2.0,
        image: "breakfast/b1009.png",
        available: true
    },
    {
        item_code: "b1010",
        name: "Tomato Soup",
        category: "breakfast",
        price: 1.6,
        image: "breakfast/b1010.png",
        available: true
    },
    {
        item_code: "b1011",
        name: "Strawberry Salad",
        category: "breakfast",
        price: 2.5,
        image: "breakfast/b1011.png",
        available: true
    },
    {
        item_code: "b1012",
        name: "Mix Stuff",
        category: "breakfast",
        price: 2.0,
        image: "breakfast/b1012.png",
        available: true
    },
    {
        item_code: "b1013",
        name: "Choko Ice",
        category: "breakfast",
        price: 2.0,
        image: "breakfast/b1013.png",
        available: true
    }
])
# Lunch
db.item_master.insertMany([
    {
        item_code: "l1001",
        name: "Pork Capsicum",
        category: "lunch",
        price: 3.5,
        image: "lunch/l1001.png",
        available: true
    },
    {
        item_code: "l1002",
        name: "Rolls",
        category: "lunch",
        price: 1.9,
        image: "lunch/l1002.png",
        available: true
    },
    {
        item_code: "l1003",
        name: "Green Egg",
        category: "lunch",
        price: 2.7,
        image: "lunch/l1003.png",
        available: true
    },
    {
        item_code: "l1004",
        name: "Cherry Omlet",
        category: "lunch",
        price: 2.4,
        image: "lunch/l1004.png",
        available: true
    },
    {
        item_code: "l1005",
        name: "Veg Noodles",
        category: "lunch",
        price: 3.0,
        image: "lunch/l1005.png",
        available: true
    },
    {
        item_code: "l1006",
        name: "Red Staw",
        category: "lunch",
        price: 1.8,
        image: "lunch/l1006.png",
        available: true
    },
    {
        item_code: "l1007",
        name: "Drum Stick",
        category: "lunch",
        price: 3.5,
        image: "lunch/l1007.png",
        available: true
    },
    {
        item_code: "l1008",
        name: "Kebab",
        category: "lunch",
        price: 2.8,
        image: "lunch/l1008.png",
        available: true
    },
    {
        item_code: "l1009",
        name: "Pork Slice",
        category: "lunch",
        price: 5.6,
        image: "lunch/l1009.png",
        available: true
    }
    {
        item_code: "l1010",
        name: "Beef Stock",
        category: "lunch",
        price: 4.7,
        image: "lunch/l1010.png",
        available: true
    },
    {
        item_code: "l1011",
        name: "Biryani",
        category: "lunch",
        price: 3.6,
        image: "lunch/l1011.png",
        available: true
    }
])
# Dinner
db.item_master.insertMany([
    {
        item_code: "d1001",
        name: "Meat Cheese",
        category: "dinner",
        price: 2.5,
        image: "dinner/d1001.png",
        available: true
    },
    {
        item_code: "d1002",
        name: "Eill Noodles",
        category: "dinner",
        price: 3.1,
        image: "dinner/d1002.png",
        available: true
    },
    {
        item_code: "d1003",
        name: "Meat Latula",
        category: "dinner",
        price: 2.7,
        image: "dinner/d1003.png",
        available: true
    },
    {
        item_code: "d1004",
        name: "Veg Ring",
        category: "dinner",
        price: 1.7,
        image: "dinner/d1004.png",
        available: true
    },
    {
        item_code: "d1005",
        name: "Chicken Drum Stick",
        category: "dinner",
        price: 3.2,
        image: "dinner/d1005.png",
        available: true
    },
    {
        item_code: "d1006",
        name: "Pork Conti",
        category: "dinner",
        price: 2.5,
        image: "dinner/d1006.png",
        available: true
    },
    {
        item_code: "d1007",
        name: "Veg Salad",
        category: "dinner",
        price: 2.1,
        image: "dinner/d1007.png",
        available: true
    }
])
