# lib/tasks/scrape.rake
namespace :scraper do
    desc "Run Python scraper and cleaner"
    task run: :environment do
      puts "Running Python scraper..."
  
      system("python3 lib/python/scraper.py") or raise "Scraper failed"
      system("python3 lib/python/clean.py") or raise "Cleaner failed"
  
      puts "Python scripts completed!"
      
      # Optional: Import cleaned CSV into your Gym model
      cleaned_file_path = Rails.root.join("lib", "python", "data", "processed_climbing_gyms.csv")
      require 'csv'
      CSV.foreach(cleaned_file_path, headers: true) do |row|
        gym = Gym.find_or_initialize_by(title: row['Title'], address: row['Address'])
      
        gym.opening_hours = row['Opening Hours']
        gym.contact_number = row['Contact No.']
        gym.features = row['Features']
        
        gym.save!
      end
      
      puts "Database import complete!"
    end
  end
  
  