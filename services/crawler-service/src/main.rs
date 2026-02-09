use sqlx::postgres::PgPoolOptions;
use dotenvy::dotenv;
use std::env;
use reqwest;
use scraper::{Html, Selector};
use serde_json::json;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenv().ok();
    // ১. DATABASE_URL ভেরিয়েবলটি নিশ্চিত করা
    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set in .env");
    
    // ২. ডাটাবেস কানেকশন (পোর্টে ৫৪৩২ ব্যবহার করা শ্রেয় আপনার .env অনুযায়ী)
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await?;
    println!("✅ Database Connected Successfully!");

    // ৩. ক্রলিং লজিক
    let target_url = "https://payslipaccountants.co.uk/";
    let response = reqwest::get(target_url).await?.text().await?;
    let document = Html::parse_document(&response);
    
    let title_selector = Selector::parse("title").unwrap();
    let title = document.select(&title_selector).next()
        .map(|t| t.inner_html()).unwrap_or_else(|| "No Title".to_string());

    // ৪. ডাইনামিক ওয়েবসাইট আইডি চেক (Foreign Key সমস্যা এড়াতে)
    // ডাটাবেস রিসেট করার পর আইডি ১ নাও থাকতে পারে, তাই লেটেস্ট আইডি খুঁজে নেওয়া ভালো
    let website_record = sqlx::query!("SELECT id FROM \"Website\" LIMIT 1")
        .fetch_optional(&pool)
        .await?;

    if let Some(record) = website_record {
        let website_id = record.id;
        
        // ৫. অডিট ডেটা ইনসার্ট করা
        sqlx::query!(
            "INSERT INTO \"Audit\" (status, \"reportData\", score, \"websiteId\") 
             VALUES ('completed', $1, $2, $3)",
            json!({ "title": title, "url": target_url }),
            85 as i32,
            website_id
        )
        .execute(&pool)
        .await?;

        println!("✅ Data inserted for Website ID: {} into Audit table successfully!", website_id);
    } else {
        println!("❌ Error: No Website found in database. Please add a website first via Prisma Studio.");
    }

    Ok(())
}