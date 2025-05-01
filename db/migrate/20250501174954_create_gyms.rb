class CreateGyms < ActiveRecord::Migration[8.0]
  def change
    create_table :gyms do |t|
      t.string :title
      t.string :address
      t.text :description
      t.string :opening_hours
      t.string :contact_number
      t.text :features

      t.timestamps
    end
  end
end
