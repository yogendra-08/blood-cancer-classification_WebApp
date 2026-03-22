# Supabase Storage Setup Guide

## 📦 Create Storage Buckets

You need to create four buckets in your Supabase project based on your 4 classes:

### 1. Benign Images Bucket
```sql
-- Create bucket for benign class images
INSERT INTO storage.buckets (id, name, public)
VALUES ('benign-images', 'benign-images', true);

-- Set up policies for public access
CREATE POLICY "Allow public uploads to benign-images" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'benign-images');

CREATE POLICY "Allow public downloads from benign-images" ON storage.objects
FOR SELECT USING (bucket_id = 'benign-images');
```

### 2. Malignant Pre-B Images Bucket
```sql
-- Create bucket for [Malignant] Pre-B class images
INSERT INTO storage.buckets (id, name, public)
VALUES ('malignant-preb-images', 'malignant-preb-images', true);

-- Set up policies for public access
CREATE POLICY "Allow public uploads to malignant-preb-images" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'malignant-preb-images');

CREATE POLICY "Allow public downloads from malignant-preb-images" ON storage.objects
FOR SELECT USING (bucket_id = 'malignant-preb-images');
```

### 3. Malignant Pro-B Images Bucket
```sql
-- Create bucket for [Malignant] Pro-B class images
INSERT INTO storage.buckets (id, name, public)
VALUES ('malignant-prob-images', 'malignant-prob-images', true);

-- Set up policies for public access
CREATE POLICY "Allow public uploads to malignant-prob-images" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'malignant-prob-images');

CREATE POLICY "Allow public downloads from malignant-prob-images" ON storage.objects
FOR SELECT USING (bucket_id = 'malignant-prob-images');
```

### 4. Malignant Early Pre-B Images Bucket
```sql
-- Create bucket for [Malignant] early Pre-B class images
INSERT INTO storage.buckets (id, name, public)
VALUES ('malignant-early-preb-images', 'malignant-early-preb-images', true);

-- Set up policies for public access
CREATE POLICY "Allow public uploads to malignant-early-preb-images" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'malignant-early-preb-images');

CREATE POLICY "Allow public downloads from malignant-early-preb-images" ON storage.objects
FOR SELECT USING (bucket_id = 'malignant-early-preb-images');
```

## 🔧 How to Set Up

### Option 1: Using Supabase Dashboard
1. Go to your Supabase project
2. Navigate to **Storage** section
3. Create four buckets:
   - `benign-images` (for Benign class)
   - `malignant-preb-images` (for [Malignant] Pre-B class)
   - `malignant-prob-images` (for [Malignant] Pro-B class)
   - `malignant-early-preb-images` (for [Malignant] early Pre-B class)
4. For each bucket, go to **Settings** → **Policies**
5. Add policies to allow public uploads and downloads

### Option 2: Using SQL Editor
1. Go to **SQL Editor** in Supabase Dashboard
2. Run the SQL commands above

## 📋 What This Does

- **Class-specific Storage**: Each cancer class has its own bucket
- **Smart Routing**: App automatically uploads to correct bucket based on prediction
- **Organized Training Data**: Perfect for future model training
- **Public Access**: Images can be accessed via public URLs

## 🔍 Automatic Bucket Selection

The app automatically routes images to the correct bucket:

| Predicted Class | Bucket Name |
|----------------|-------------|
| Benign | `benign-images` |
| [Malignant] Pre-B | `malignant-preb-images` |
| [Malignant] Pro-B | `malignant-prob-images` |
| [Malignant] early Pre-B | `malignant-early-preb-images` |

## 🚀 Check Your Setup

After setting up, you should see:
1. Four buckets in Storage section
2. Public URLs working for uploaded images
3. Images automatically sorted by class in correct buckets

## 📝 URLs Format

The URLs will look like:
```
https://your-project.supabase.co/storage/v1/object/public/benign-images/uuid_filename.jpg
https://your-project.supabase.co/storage/v1/object/public/malignant-preb-images/uuid_filename.jpg
https://your-project.supabase.co/storage/v1/object/public/malignant-prob-images/uuid_filename.jpg
https://your-project.supabase.co/storage/v1/object/public/malignant-early-preb-images/uuid_filename.jpg
```

This ensures all images are stored permanently in Supabase Storage and perfectly organized by class! 🎯
